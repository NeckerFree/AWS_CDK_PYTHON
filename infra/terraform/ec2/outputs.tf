output "apache_public_ip" {
  description = "Public IP of the Apache server"
  value       = aws_instance.apache_server.public_ip
}
