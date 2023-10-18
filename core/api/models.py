from django.db import models

# Create your models here.

# service item park (Only Update Table)
class SVC_I_PARK(models.Model):
    AN = models.IntegerField()

    PC = models.BooleanField(
        default=False
    )

    # Parking Time
    PT = models.IntegerField(
        default=0
    )

    type = models.ForeignKey(
        'api.SVC_T_PARK',
        on_delete=models.CASCADE,
    )

    created_data = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)



# service type park
class SVC_T_PARK(models.Model):
    type = models.IntegerField()

    name = models.CharField(
        max_length=20,
    )