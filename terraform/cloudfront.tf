# ══════════════════════════════════════════════
#  CloudFront Function — Maintenance Mode
# ══════════════════════════════════════════════

resource "aws_cloudfront_function" "maintenance" {
  name    = "${local.name_prefix}-maintenance"
  runtime = "cloudfront-js-2.0"
  comment = "Maintenance mode for ${local.env}"
  publish = true

  code = <<-JSEOF
    function handler(event) {
      return {
        statusCode: 503,
        statusDescription: "Service Temporarily Unavailable",
        headers: {
          "content-type": { value: "text/html; charset=UTF-8" },
          "retry-after": { value: "3600" },
          "cache-control": { value: "no-store, no-cache, must-revalidate" }
        },
        body: [
          '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
          '<title>VedicJivan - We will be back soon</title>',
          '<style>',
          '*{margin:0;padding:0;box-sizing:border-box}',
          'body{min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:#0f0f1a;color:#fff;overflow:hidden}',
          '.bg{position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse at 50% 50%,#1a1530 0%,#0f0f1a 70%);z-index:0}',
          '.stars{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1}',
          '.star{position:absolute;border-radius:50%;background:#fde68a;animation:twinkle var(--d,3s) ease-in-out infinite alternate}',
          '@keyframes twinkle{0%%{opacity:.2;transform:scale(.8)}100%%{opacity:1;transform:scale(1.2)}}',
          '.container{position:relative;z-index:2;text-align:center;padding:2rem;max-width:560px}',
          '.logo-wrap{margin-bottom:2rem;animation:floatUp 3s ease-in-out infinite alternate}',
          '.logo-wrap svg{width:120px;height:120px;filter:drop-shadow(0 0 20px rgba(245,158,11,.4))}',
          '@keyframes floatUp{0%%{transform:translateY(5px)}100%%{transform:translateY(-5px)}}',
          '.brand{font-size:2.2rem;font-weight:700;background:linear-gradient(135deg,#fde68a,#f59e0b,#d97706);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.5rem;letter-spacing:1px}',
          '.divider{width:80px;height:2px;background:linear-gradient(90deg,transparent,#f59e0b,transparent);margin:1.2rem auto;animation:glow 2s ease-in-out infinite alternate}',
          '@keyframes glow{0%%{opacity:.5;width:60px}100%%{opacity:1;width:100px}}',
          'h1{font-size:1.5rem;font-weight:400;color:#e2e8f0;margin-bottom:.75rem}',
          'p{font-size:1rem;line-height:1.7;color:#94a3b8;margin-bottom:.5rem}',
          '.contact{margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid rgba(245,158,11,.15)}',
          '.contact a{color:#fbbf24;text-decoration:none;transition:color .2s}',
          '.contact a:hover{color:#fde68a}',
          '.spinner{display:inline-block;width:20px;height:20px;border:2px solid rgba(245,158,11,.3);border-top-color:#f59e0b;border-radius:50%;animation:spin 1s linear infinite;margin-right:8px;vertical-align:middle}',
          '@keyframes spin{to{transform:rotate(360deg)}}',
          '.status{display:inline-flex;align-items:center;margin-top:1.5rem;padding:.5rem 1.2rem;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.2);border-radius:2rem;font-size:.85rem;color:#fbbf24}',
          '</style></head><body>',
          '<div class="bg"></div>',
          '<div class="stars">',
          '<div class="star" style="top:10%;left:15%;width:3px;height:3px;--d:2.5s"></div>',
          '<div class="star" style="top:20%;left:80%;width:2px;height:2px;--d:4s"></div>',
          '<div class="star" style="top:35%;left:5%;width:2px;height:2px;--d:3.5s"></div>',
          '<div class="star" style="top:50%;left:90%;width:3px;height:3px;--d:2s"></div>',
          '<div class="star" style="top:65%;left:25%;width:2px;height:2px;--d:4.5s"></div>',
          '<div class="star" style="top:75%;left:70%;width:3px;height:3px;--d:3s"></div>',
          '<div class="star" style="top:85%;left:45%;width:2px;height:2px;--d:2.8s"></div>',
          '<div class="star" style="top:15%;left:55%;width:2px;height:2px;--d:3.2s"></div>',
          '<div class="star" style="top:45%;left:40%;width:3px;height:3px;--d:3.8s"></div>',
          '<div class="star" style="top:90%;left:85%;width:2px;height:2px;--d:2.2s"></div>',
          '</div>',
          '<div class="container">',
          '<div class="logo-wrap">',
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-110 -120 220 220"><defs><linearGradient id="gO" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#fbbf24"/><stop offset="100%" style="stop-color:#d97706"/></linearGradient><linearGradient id="gM" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#fcd34d"/><stop offset="100%" style="stop-color:#f59e0b"/></linearGradient><linearGradient id="gI" x1="0%" y1="20%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#fde68a"/><stop offset="100%" style="stop-color:#fbbf24"/></linearGradient><linearGradient id="gL" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" style="stop-color:#fde68a"/><stop offset="100%" style="stop-color:#f59e0b"/></linearGradient></defs><g><path d="M0,-85 C-18,-75 -22,-45 -18,-25 C-12,-5 -5,5 0,10 C5,5 12,-5 18,-25 C22,-45 18,-75 0,-85Z" fill="url(#gO)" opacity=".85"/><path d="M0,-85 C-18,-75 -22,-45 -18,-25 C-12,-5 -5,5 0,10 C5,5 12,-5 18,-25 C22,-45 18,-75 0,-85Z" fill="url(#gO)" opacity=".8" transform="rotate(72)"/><path d="M0,-85 C-18,-75 -22,-45 -18,-25 C-12,-5 -5,5 0,10 C5,5 12,-5 18,-25 C22,-45 18,-75 0,-85Z" fill="url(#gO)" opacity=".75" transform="rotate(144)"/><path d="M0,-85 C-18,-75 -22,-45 -18,-25 C-12,-5 -5,5 0,10 C5,5 12,-5 18,-25 C22,-45 18,-75 0,-85Z" fill="url(#gO)" opacity=".75" transform="rotate(216)"/><path d="M0,-85 C-18,-75 -22,-45 -18,-25 C-12,-5 -5,5 0,10 C5,5 12,-5 18,-25 C22,-45 18,-75 0,-85Z" fill="url(#gO)" opacity=".8" transform="rotate(288)"/><path d="M0,-65 C-14,-56 -17,-34 -14,-18 C-9,-4 -4,3 0,7 C4,3 9,-4 14,-18 C17,-34 14,-56 0,-65Z" fill="url(#gM)" opacity=".9" transform="rotate(36)"/><path d="M0,-65 C-14,-56 -17,-34 -14,-18 C-9,-4 -4,3 0,7 C4,3 9,-4 14,-18 C17,-34 14,-56 0,-65Z" fill="url(#gM)" opacity=".88" transform="rotate(108)"/><path d="M0,-65 C-14,-56 -17,-34 -14,-18 C-9,-4 -4,3 0,7 C4,3 9,-4 14,-18 C17,-34 14,-56 0,-65Z" fill="url(#gM)" opacity=".85" transform="rotate(180)"/><path d="M0,-65 C-14,-56 -17,-34 -14,-18 C-9,-4 -4,3 0,7 C4,3 9,-4 14,-18 C17,-34 14,-56 0,-65Z" fill="url(#gM)" opacity=".85" transform="rotate(252)"/><path d="M0,-65 C-14,-56 -17,-34 -14,-18 C-9,-4 -4,3 0,7 C4,3 9,-4 14,-18 C17,-34 14,-56 0,-65Z" fill="url(#gM)" opacity=".88" transform="rotate(324)"/><path d="M0,-42 C-9,-35 -11,-20 -9,-10 C-6,-2 -3,2 0,4 C3,2 6,-2 9,-10 C11,-20 9,-35 0,-42Z" fill="url(#gI)" opacity=".95" transform="rotate(18)"/><path d="M0,-42 C-9,-35 -11,-20 -9,-10 C-6,-2 -3,2 0,4 C3,2 6,-2 9,-10 C11,-20 9,-35 0,-42Z" fill="url(#gI)" opacity=".93" transform="rotate(90)"/><path d="M0,-42 C-9,-35 -11,-20 -9,-10 C-6,-2 -3,2 0,4 C3,2 6,-2 9,-10 C11,-20 9,-35 0,-42Z" fill="url(#gI)" opacity=".9" transform="rotate(162)"/><path d="M0,-42 C-9,-35 -11,-20 -9,-10 C-6,-2 -3,2 0,4 C3,2 6,-2 9,-10 C11,-20 9,-35 0,-42Z" fill="url(#gI)" opacity=".9" transform="rotate(234)"/><path d="M0,-42 C-9,-35 -11,-20 -9,-10 C-6,-2 -3,2 0,4 C3,2 6,-2 9,-10 C11,-20 9,-35 0,-42Z" fill="url(#gI)" opacity=".93" transform="rotate(306)"/><circle cx="0" cy="0" r="12" fill="url(#gL)"/><circle cx="0" cy="0" r="8" fill="#fde68a" opacity=".9"/><circle cx="0" cy="0" r="4" fill="#fff" opacity=".5"/></g></svg>',
          '</div>',
          '<div class="brand">VedicJivan</div>',
          '<div class="divider"></div>',
          '<h1>We will be back soon</h1>',
          '<p>We are undergoing scheduled maintenance to improve your experience. Everything will be back to normal shortly.</p>',
          '<div class="status"><span class="spinner"></span>Maintenance in progress</div>',
          '<div class="contact"><p>For urgent enquiries, please reach out at<br><a href="mailto:vedic.jivan33@gmail.com">vedic.jivan33@gmail.com</a></p></div>',
          '</div></body></html>'
        ].join('')
      };
    }
  JSEOF
}


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

    # Maintenance mode OR basic auth — only one viewer-request function allowed
    dynamic "function_association" {
      for_each = var.maintenance_mode ? [1] : (var.test_site_username != "" ? [1] : [])
      content {
        event_type   = "viewer-request"
        function_arn = var.maintenance_mode ? aws_cloudfront_function.maintenance.arn : aws_cloudfront_function.basic_auth[0].arn
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
