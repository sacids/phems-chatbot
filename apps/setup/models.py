from django.db import models

# Create your models here.
#regions
class Region(models.Model):
    name       = models.CharField(max_length=30, blank = False, null = False)
    dictionary = models.TextField(null=True, blank=True)
    view_id    = models.IntegerField(null=True, blank=True)  

    class Meta:
        db_table     = 'ph_regions'
        managed      = True
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return str(self.name)

#districts
class District(models.Model):
    name       = models.CharField(max_length=30, blank = False, null = False)
    region     = models.ForeignKey(Region, related_name='district', on_delete=models.DO_NOTHING)
    dictionary = models.TextField(null=True, blank=True)
    view_id    = models.IntegerField(null=True, blank=True)  

    class Meta: 
        db_table = 'ph_districts'
        managed  = True
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    def __str__(self):
        return str(self.name)

#wards
class Ward(models.Model):
    name       = models.CharField(max_length=30,blank=False, null=False)
    district   = models.ForeignKey(District, related_name='ward',on_delete=models.DO_NOTHING)  
    dictionary = models.TextField(null=True, blank=True)
    view_id    = models.IntegerField(null=True, blank=True)  

    class Meta: 
        db_table  =  'ph_wards'
        managed   =  True
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'  

    def __str__(self):
        return str(self.name)


class Village(models.Model):
    name         = models.CharField(max_length=30, null=False, blank=False)
    ward         = models.ForeignKey(Ward, related_name='village', on_delete=models.DO_NOTHING)
    dictionary   = models.TextField(null=True, blank=True)
    view_id      = models.IntegerField(null=True, blank=True)  

    class Meta:
        db_table = 'ph_villages'
        managed  = True
        verbose_name  = 'Village'
        verbose_name_plural = 'Villages'  

    def __str__(self):
        return str(self.name)   


class Hamlet(models.Model):
    name         = models.CharField(max_length=30, null=False, blank=False)
    village      = models.ForeignKey(Village, related_name='hamlet', on_delete=models.DO_NOTHING)
    dictionary   = models.TextField(null=True, blank=True)
    view_id      = models.IntegerField(null=True, blank=True)  

    class Meta:
        db_table  = 'ph_hamlets'
        managed   = True
        verbose_name = 'Hamlet'
        verbose_name_plural = 'Hamlets' 

    def __str__(self):
        return str(self.name) 
