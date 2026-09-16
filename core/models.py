from django.db import models

# Create your models here.

class ImpactProject(models.Model):
    IMPACT_AREAS=[
        ('education', 'Education'),
        ('health', 'Health'),
        ('agriculture', 'Agriculture'),
        ('environment', 'Environment'),
        ('technology', 'Technology'),
        ('employment', 'Employment'),
        ('other', 'Other'),
        ]
    STATUS_CHOICES=[
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    name = models.CharField(max_length = 200)
    description = models.TextField()


    country = models.CharField(max_length=100)
    location = models.CharField(max_length=200)


    impact_area = models.CharField(max_length=50, choices=IMPACT_AREAS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned',)


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class ImpactRecord(models.Model):
    project = models.ForeignKey(
        ImpactProject,
        on_delete=models.CASCADE,
        related_name = "impact_records",
    )

    metric = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=50)

    recorded_at = models.DateField()

    def __str__(self):
        return f"{self.metric} - {self.value} {self.unit}"
    
