import UIKit
import NativeCmpKitWebViewConsumer

@main
final class ConsumerApp: UIResponder, UIApplicationDelegate {
    var window: UIWindow?

    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let host = UIWindow(frame: UIScreen.main.bounds)
        host.rootViewController = WebViewConsumerKt.createConsumerController { message in
            FileHandle.standardOutput.write(Data("\(message)\n".utf8))
        }
        window = host
        host.makeKeyAndVisible()
        return true
    }
}
