# ── ECS Auto Scaling ──
# Budget-friendly: 1 task normally, scales to 2 only under sustained load.

resource "aws_appautoscaling_target" "api" {
  max_capacity       = 2
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.api.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# Scale on CPU — add task if CPU > 75% for 3 minutes
resource "aws_appautoscaling_policy" "api_cpu" {
  name               = "${lower(var.project_name)}-api-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.api.resource_id
  scalable_dimension = aws_appautoscaling_target.api.scalable_dimension
  service_namespace  = aws_appautoscaling_target.api.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 75
    scale_in_cooldown  = 300 # Wait 5 min before scaling down
    scale_out_cooldown = 120 # Wait 2 min before scaling up again
  }
}
