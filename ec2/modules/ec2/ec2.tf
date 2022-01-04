resource "aws_instance" "web" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = var.vpc_security_group
  subnet_id              = var.subnet_id

  tags = {
    Name        = var.name
    Project     = "Mythril"
    Environment = var.environment
  }
}