resource "aws_instance" "apache_server" {
  ami           = "ami-0866a3c8686eaeeba" # Ubuntu
  instance_type = var.instance_type
  key_name      = var.key_name

user_data = <<-EOF
            #!/bin/bash
            sudo apt update -y
            sudo apt install apache2 -y
            sudo ufw allow 'Apache'
            sudo ufw --force enable  # Ensure the firewall is enabled
            sudo systemctl start apache2
            sudo systemctl enable apache2
            echo "Welcome to Apache server on AWS" | sudo tee /var/www/html/index.html
            EOF

  tags = {
    Name = "Apache_Server"
  }

  # Add security group for HTTP traffic
  vpc_security_group_ids = [aws_security_group.allow_http.id]

  associate_public_ip_address = true

  subnet_id = aws_subnet.public_subnet.id
}
