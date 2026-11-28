"""Owned loopback peer for a real TLS HTTP/2 stream cancellation witness."""

import argparse
import json
from pathlib import Path
import socket
import ssl
import time

from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.errors import ErrorCodes
from h2.events import RequestReceived, StreamReset


def mark(directory, name, value):
    temporary = directory / f"{name}.part"
    temporary.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(directory / name)


def send_document(connection, stream, title):
    payload = f'<html><head><link rel="icon" href="data:,"><title>{title}</title></head><body>ok</body></html>'.encode()
    connection.send_headers(stream, [(":status", "200"), ("content-type", "text/html; charset=utf-8"),
                                     ("content-length", str(len(payload))), ("cache-control", "no-store")])
    connection.send_data(stream, payload, end_stream=True)


def serve(directory, certificate, key):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certificate, key)
    context.set_alpn_protocols(["h2"])
    with socket.create_server(("127.0.0.1", 0), backlog=1) as listener:
        listener.settimeout(15)
        port = listener.getsockname()[1]
        mark(directory, "port.json", port)
        plain, _ = listener.accept()
    plain.settimeout(10)
    with plain, context.wrap_socket(plain, server_side=True) as wire:
        if wire.selected_alpn_protocol() != "h2":
            raise ValueError("The actual client must negotiate HTTP/2")
        wire.settimeout(0.25)
        http = H2Connection(H2Configuration(client_side=False, header_encoding="utf-8"))
        http.initiate_connection()
        wire.sendall(http.data_to_send())
        streams, reset, recovered = {}, None, False
        expected_paths = ("/cancel", "/survive", "/recover")
        deadline = time.monotonic() + 40
        while time.monotonic() < deadline:
            if recovered and (directory / "client-complete").is_file():
                return {"alpn": "h2", "single_connection": True, "cancelled_stream": reset,
                        "other_stream": streams["/survive"], "recovery_stream": streams["/recover"],
                        "reset_code": int(ErrorCodes.CANCEL), "response_started_before_cancel": False}
            try:
                data = wire.recv(65536)
            except TimeoutError:
                continue
            if not data:
                raise ValueError("The HTTP/2 connection closed before the sibling and recovery completed")
            for event in http.receive_data(data):
                if isinstance(event, RequestReceived):
                    headers = dict(event.headers)
                    index = len(streams)
                    if (index >= len(expected_paths) or headers.get(":path") != expected_paths[index] or
                            headers.get(":method") != "GET" or headers.get(":authority") != f"127.0.0.1:{port}"):
                        raise ValueError("Unexpected owned HTTP/2 request")
                    streams[expected_paths[index]] = event.stream_id
                    if index == 0:
                        mark(directory, "cancel-pending", event.stream_id)
                    elif index == 1:
                        mark(directory, "both-pending", sorted(streams.values()))
                    else:
                        if reset is None:
                            raise ValueError("Recovery preceded the real stream reset")
                        send_document(http, event.stream_id, "NativeCmpKitH2Recovery")
                        recovered = True
                elif isinstance(event, StreamReset):
                    if (reset is not None or len(streams) != 2 or not event.remote_reset or
                            event.stream_id != streams["/cancel"] or event.error_code != ErrorCodes.CANCEL):
                        raise ValueError("Expected a single peer CANCEL reset for the held stream only")
                    reset = event.stream_id
                    send_document(http, streams["/survive"], "NativeCmpKitH2Survived")
            wire.sendall(http.data_to_send())
    raise TimeoutError("The real HTTP/2 stream reset or recovery did not finish before the deadline")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("key", type=Path)
    args = parser.parse_args()
    mark(args.directory, "peer.json", serve(args.directory, args.certificate, args.key))
