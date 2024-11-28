# outputs.tf
output "app_instance_ip" {
  value = aws_instance.app_server.public_ip
}

output "ecr_repository_url" {
  value = aws_ecr_repository.platyfin.repository_url
}

output "route53_zone_id" {
  value = aws_route53_zone.main.zone_id
}

output "route53_record_name" {
  value = aws_route53_record.www.name
}