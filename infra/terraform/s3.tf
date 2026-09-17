resource "aws_s3_bucket" "order_data" {
  bucket = "orderflow-order-data-prod"
  acl    = "public-read"
}

resource "aws_s3_bucket_versioning" "order_data" {
  bucket = aws_s3_bucket.order_data.id
  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket" "audit_logs" {
  bucket = "orderflow-audit-logs-prod"
  acl    = "public-read"
}
