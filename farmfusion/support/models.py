from django.db import models
from accounts.models import CustomUser  # Import the CustomUser model
from businessmodel.models import InvestmentModel  # Import the InvestmentModel

class SupportPost(models.Model):
    amount = models.BigIntegerField(default=0)  # Amount contributed
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="support_posts")  # The user who made the contribution
    investmodel = models.ForeignKey(InvestmentModel, on_delete=models.CASCADE, related_name="support_posts")  # The model being supported

    def __str__(self):
        return f"SupportPost by {self.user.username} for {self.investmodel.name}"
