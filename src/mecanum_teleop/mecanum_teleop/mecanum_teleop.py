import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import curses
import threading
import time

class MecanumTeleopCurses(Node):
    def __init__(self):
        super().__init__('mecanum_teleop_curses')
        self.publisher = self.create_publisher(TwistStamped, '/mecanum_drive_controller/cmd_vel', 10)
        self.speed = 0.2
        self.speed_rotation = 0.5
        self.key = None
        self.lock = threading.Lock()

        self.running = True

        # Start curses input in separate thread
        self.thread = threading.Thread(target=self.keyboard_loop)
        self.thread.daemon = True
        self.thread.start()

        # Timer to publish messages regularly
        self.timer = self.create_timer(0.05, self.publish_command)

        self.get_logger().info(
            "Teleop started (using curses).\n"
            "Use WASD to move, Q/E to rotate, SPACE to stop, ESC to exit."
        )

        self.linear_x = 0.0
        self.linear_y = 0.0
        self.angular_z = 0.0

    def keyboard_loop(self):
        def curses_loop(stdscr):
            stdscr.nodelay(True)
            stdscr.keypad(True)
            while self.running:
                try:
                    c = stdscr.getch()
                    with self.lock:
                        self.key = c
                except Exception:
                    pass
                time.sleep(0.05)

        curses.wrapper(curses_loop)

    def publish_command(self):
        key = None
        with self.lock:
            key = self.key
            self.key = None  # clear key after reading

        if key is None:
            # If no key pressed, maintain current state
            pass
        else:
            # Map keys to actions
            if key in [ord('w'), ord('W')]:
                self.linear_x = self.speed
            elif key in [ord('s'), ord('S')]:
                self.linear_x = -self.speed
            elif key in [ord('a'), ord('A')]:
                self.linear_y = self.speed
            elif key in [ord('d'), ord('D')]:
                self.linear_y = -self.speed
            elif key in [ord('q'), ord('Q')]:
                self.angular_z = self.speed_rotation
            elif key in [ord('e'), ord('E')]:
                self.angular_z = -self.speed_rotation
            elif key == ord(' '):
                self.linear_x = 0.0
                self.linear_y = 0.0
                self.angular_z = 0.0
            elif key == 27:  # ESC
                self.get_logger().info('ESC pressed. Exiting...')
                self.running = False
                rclpy.shutdown()

        twist = TwistStamped()
        twist.header.stamp = self.get_clock().now().to_msg()
        twist.twist.linear.x = self.linear_x
        twist.twist.linear.y = self.linear_y
        twist.twist.angular.z = self.angular_z
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = MecanumTeleopCurses()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.running = False
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
