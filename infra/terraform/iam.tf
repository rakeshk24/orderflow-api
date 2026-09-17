resource "aws_iam_role" "order_service" {
  name = "orderflow-order-service"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "order_service" {
  name = "orderflow-order-service-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "order_service" {
  role       = aws_iam_role.order_service.name
  policy_arn = aws_iam_policy.order_service.arn
}

resource "aws_iam_policy" "api_gateway_s3" {
  name = "orderflow-api-gateway-s3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:*"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:*"]
        Resource = "*"
      }
    ]
  })
}
