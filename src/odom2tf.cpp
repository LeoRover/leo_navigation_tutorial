#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>

static std::string topic = "odometry_merged";

void odom_callback(const nav_msgs::OdometryConstPtr& odom){
  static tf::TransformBroadcaster br;
  tf::Transform tf;
  geometry_msgs::Pose odom_pose = odom->pose.pose;
  tf::poseMsgToTF(odom_pose, tf);

  tf::StampedTransform stamped_tf(tf, odom->header.stamp, odom->header.frame_id, "base_footprint");

  br.sendTransform(stamped_tf);
}

int main(int argc, char **argv){

  ros::init(argc, argv, "odom2tf");
  ros::NodeHandle nh;
  ros::NodeHandle pnh("~");

  pnh.getParam("odom_topic", topic);

  ros::Subscriber odom_sub = nh.subscribe(topic, 10, odom_callback);
  ros::spin();

  return 0;
}