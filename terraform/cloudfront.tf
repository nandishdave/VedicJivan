# ══════════════════════════════════════════════
#  CloudFront Function — Basic Auth (test env only)
# ══════════════════════════════════════════════

resource "aws_cloudfront_function" "basic_auth" {
  count   = var.test_site_username != "" ? 1 : 0
  name    = "${local.name_prefix}-basic-auth"
  runtime = "cloudfront-js-2.0"
  comment = "Basic auth for ${local.env} environment"
  publish = true

  code = <<-JSEOF
    var EXPECTED = "Basic ${base64encode("${var.test_site_username}:${var.test_site_password}")}";

    function handler(event) {
      var request = event.request;
      var headers = request.headers;

      if (!headers.authorization || headers.authorization.value !== EXPECTED) {
        return {
          statusCode: 401,
          statusDescription: "Unauthorized",
          headers: {
            "www-authenticate": { value: 'Basic realm="VedicJivan Test"' }
          }
        };
      }

      return request;
    }
  JSEOF
}


# ══════════════════════════════════════════════
#  Response Headers Policy — noindex (test env only)
# ══════════════════════════════════════════════

resource "aws_cloudfront_response_headers_policy" "noindex" {
  count   = terraform.workspace != "default" ? 1 : 0
  name    = "${local.name_prefix}-noindex"
  comment = "Prevent search engine indexing for ${local.env}"

  custom_headers_config {
    items {
      header   = "X-Robots-Tag"
      value    = "noindex, nofollow, noarchive"
      override = true
    }
  }
}


# ══════════════════════════════════════════════
#  CloudFront Distribution
# ══════════════════════════════════════════════

resource "aws_cloudfront_distribution" "website" {
  enabled             = true
  default_root_object = "index.html"
  comment             = "${var.project_name} ${local.env} Static Website"
  aliases             = [local.frontend_domain]
  http_version        = "http2and3"

  origin {
    domain_name = aws_s3_bucket_website_configuration.website.website_endpoint
    origin_id   = "S3-${aws_s3_bucket.website.id}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-${aws_s3_bucket.website.id}"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 86400
    max_ttl     = 31536000

    # Basic auth — only attached for test env
    dynamic "function_association" {
      for_each = var.test_site_username != "" ? [1] : []
      content {
        event_type   = "viewer-request"
        function_arn = aws_cloudfront_function.basic_auth[0].arn
      }
    }

    # noindex headers — only attached for non-prod
    response_headers_policy_id = terraform.workspace != "default" ? aws_cloudfront_response_headers_policy.noindex[0].id : null
  }

  # 403 -> custom 404 page
  custom_error_response {
    error_code            = 403
    response_code         = 404
    response_page_path    = "/404/index.html"
    error_caching_min_ttl = 10
  }

  # 404 -> custom 404 page
  custom_error_response {
    error_code            = 404
    response_code         = 404
    response_page_path    = "/404/index.html"
    error_caching_min_ttl = 10
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn != "" ? var.acm_certificate_arn : aws_acm_certificate_validation.frontend[0].certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  tags = local.common_tags
}
