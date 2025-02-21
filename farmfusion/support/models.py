from django.db import models
from accounts.models import CustomUser  # Import the CustomUser model from the accounts app
from businessmodel.models import InvestmentModel  # Import the InvestmentModel from the businessmodel app

class SupportPost(models.Model):
    requiredamount = models.BigIntegerField()  # Amount required to support the investment
    amount = models.BigIntegerField()  # Actual amount contributed to the investment
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="support_posts")  # The user who is making the support
    investmodel = models.ForeignKey(InvestmentModel, on_delete=models.CASCADE, related_name="support_posts")  # The investment model being supported

    def __str__(self):
        return f"SupportPost by {self.user.username} for {self.investmodel.name}"
