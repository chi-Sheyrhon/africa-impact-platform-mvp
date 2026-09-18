from django.db import models

# Create your models here.

class ImpactProject(models.Model):
    AFRICAN_COUNTRIES=[
         ("Algeria", "Algeria"),
        ("Angola", "Angola"),
        ("Benin", "Benin"),
        ("Botswana", "Botswana"),
        ("Burkina Faso", "Burkina Faso"),
        ("Burundi", "Burundi"),
        ("Cabo Verde", "Cabo Verde"),
        ("Cameroon", "Cameroon"),
        ("Central African Republic", "Central African Republic"),
        ("Chad", "Chad"),
        ("Comoros", "Comoros"),
        ("Democratic Republic of the Congo", "Democratic Republic of the Congo"),
        ("Republic of the Congo", "Republic of the Congo"),
        ("Cote d'Ivoire", "Cote d'Ivoire"),
        ("Djibouti", "Djibouti"),
        ("Egypt", "Egypt"),
        ("Equatorial Guinea", "Equatorial Guinea"),
        ("Eritrea", "Eritrea"),
        ("Eswatini", "Eswatini"),
        ("Ethiopia", "Ethiopia"),
        ("Gabon", "Gabon"),
        ("Gambia", "Gambia"),
        ("Ghana", "Ghana"),
        ("Guinea", "Guinea"),
        ("Guinea-Bissau", "Guinea-Bissau"),
        ("Kenya", "Kenya"),
        ("Lesotho", "Lesotho"),
        ("Liberia", "Liberia"),
        ("Libya", "Libya"),
        ("Madagascar", "Madagascar"),
        ("Malawi", "Malawi"),
        ("Mali", "Mali"),
        ("Mauritania", "Mauritania"),
        ("Mauritius", "Mauritius"),
        ("Morocco", "Morocco"),
        ("Mozambique", "Mozambique"),
        ("Namibia", "Namibia"),
        ("Niger", "Niger"),
        ("Nigeria", "Nigeria"),
        ("Rwanda", "Rwanda"),
        ("Sao Tome and Principe", "Sao Tome and Principe"),
        ("Senegal", "Senegal"),
        ("Seychelles", "Seychelles"),
        ("Sierra Leone", "Sierra Leone"),
        ("Somalia", "Somalia"),
        ("South Africa", "South Africa"),
        ("South Sudan", "South Sudan"),
        ("Sudan", "Sudan"),
        ("Tanzania", "Tanzania"),
        ("Togo", "Togo"),
        ("Tunisia", "Tunisia"),
        ("Uganda", "Uganda"),
        ("Zambia", "Zambia"),
        ("Zimbabwe", "Zimbabwe"),
    ]
    
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


    country = models.CharField(
        max_length=100,
        choices=AFRICAN_COUNTRIES,)
    location = models.CharField(max_length=200)


    impact_area = models.CharField(
        max_length=50,
        choices=IMPACT_AREAS,
        )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned",
        )


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class ImpactRecord(models.Model):

    METRIC_CATEGORIES = [
        ("people", "People"),
        ("education", "Education"),
        ("health", "Health"),
        ("infrastructure", "Infrastructure"),
        ("employment", "Employment"),
        ("agriculture", "Agriculture"),
        ("community", "Community"),
        ("environment", "Environment"),
        ("other", "Other"),
    ]

    project = models.ForeignKey(
        ImpactProject,
        on_delete=models.CASCADE,
        related_name="impact_records",
    )

    metric = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=50,
        choices=METRIC_CATEGORIES,
        default="other",
    )

    value = models.FloatField()

    unit = models.CharField(
        max_length=50
    )

    recorded_at = models.DateField()

    def __str__(self):
        return f"{self.metric} - {self.value} {self.unit}"
    
