from django.db import models
from accounts.models import CustomUser

class Farmer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="farmer")
    land_area = models.BigIntegerField(default = 0)
    soil_type = models.CharField(max_length=255,null=True,default=0)
    crop_type = models.CharField(max_length=255,null=True,default=0)
    farm_type = models.CharField(max_length=255,null=True,default="farmer")
    token = models.BigIntegerField(default = 100)
    def __str__(self):
        return f"Farmer: {self.user.username}"
    
class Investor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="investor")
    total_invested = models.IntegerField(default=0)
    total_investments = models.IntegerField(default=0)
    active_investments = models.IntegerField(default=0)

    def __str__(self):
        return f"Investor: {self.user.username}"

class InvestmentModel(models.Model):
    name = models.CharField(max_length=255)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="investments")
    capital = models.BigIntegerField()
    farmer_share = models.IntegerField()
    requiredamount = models.BigIntegerField(default=0)
    working_share = models.BigIntegerField()
    estimated_time = models.CharField()
    is_disbursed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    profit_generated = models.IntegerField(null=True, blank=True,default=0)
    is_verified = models.BooleanField(null=True)
    def __str__(self):
        return f"Investment: {self.name} by {self.farmer.user.username}"
class Investment(models.Model):
    investment_model = models.ForeignKey(InvestmentModel, on_delete=models.CASCADE, related_name="investments")
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="investments")
    investment_amount = models.IntegerField()

    def __str__(self):
        return f"{self.investor.user.username} invested in {self.investment_model.name}"
class verifymodel(models.Model):
    investment_model = models.ForeignKey(InvestmentModel, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crpimg=models.ImageField(upload_to='product_images/')
    iasimg=models.ImageField(upload_to='product_images/')
    doc_number=models.BigIntegerField()
    articleimg=models.ImageField(upload_to='product_images/')
    artlink=models.CharField(max_length=255)
    is_approved = models.BooleanField(null=True)
class VerificationQuery(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="verification_queries")
    investment_model = models.ForeignKey(InvestmentModel, on_delete=models.CASCADE, related_name="verification_queries")
    verifymodel = models.ForeignKey(verifymodel, on_delete=models.CASCADE, related_name="queries", null=True, blank=True)
    reason = models.TextField()  # Farmer's reason for verification failure
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[("pending", "Pending"), ("resolved", "Resolved")], 
        default="pending"
    )

    def __str__(self):
        return f"Query by {self.farmer.user.username} on {self.investment_model.name}"
