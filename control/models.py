from django.db import models


class Sucursal(models.Model):

    nombre = models.CharField(max_length=50)
    gerente = models.CharField(max_length=50, blank = True)
    calle = models.CharField(max_length=50, blank = True)
    num = models.CharField(max_length=5, blank = True)
    num_int = models.CharField(max_length=5, blank = True)
    cp = models.CharField(max_length=5, blank = True)
    col = models.CharField(max_length=30, blank = True)
    mun = models.CharField(max_length=30, blank = True)
    estado = models.CharField(max_length=20, blank = True)
    tel = models.CharField(max_length=13, blank = True)
    
    class Meta:
        db_table = "sucursal"

class Personal(models.Model):
    nombre = models.CharField(max_length=50)
    apellido_pat = models.CharField(max_length=30)
    apellido_mat = models.CharField(max_length=30, blank = True)
    sucursal = models.ForeignKey(Sucursal,on_delete=models.CASCADE)
    sexo = models.CharField(max_length=1, blank = True)
    fecha_nac = models.CharField(max_length=10, blank = True)
    curp = models.CharField(max_length=18, blank = True)
    rfc = models.CharField(max_length=18, blank = True)
    nss = models.CharField(max_length=18, blank = True)
    calle = models.CharField(max_length=50, blank = True)
    num = models.CharField(max_length=5, blank = True)
    num_int = models.CharField(max_length=5, blank = True)
    cp = models.CharField(max_length=5, blank = True)
    col = models.CharField(max_length=30, blank = True)
    mun = models.CharField(max_length=30, blank = True)
    estado = models.CharField(max_length=20, blank = True)
    tel_celu = models.CharField(max_length=13, blank = True)
    tel_otro = models.CharField(max_length=13, blank = True)
    email = models.EmailField(max_length=100, blank = True)
    alias = models.CharField(max_length=30)
    nip = models.CharField(max_length=4, blank = True)
    activo = models.BooleanField(default = True)
    
    
    class Meta:
        db_table = "personal"

class ControlHoras(models.Model):
    trabajador = models.ForeignKey(Personal,on_delete=models.CASCADE)
    #sucursal = models.ForeignKey(Sucursal,on_delete=models.CASCADE)
    fecha = models.DateField(blank = True, null = True)
    hora_entrada = models.TimeField(blank = True, null = True)
    hora_salida = models.TimeField(blank = True, null = True)
    hora_comidai = models.TimeField(blank = True, null = True)
    hora_comidaf = models.TimeField(blank = True, null = True)
    #justificado = models.BooleanField(default = False)
    
    class Meta:
        db_table = "controlhoras"