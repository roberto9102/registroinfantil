from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'password',
            #'first_name',
            #'last_name',
            #'email',
            'rol',
            'personal',
            'madre',
            'is_active',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined',  ]

    def validate(self, attrs):
        rol = attrs.get('rol', getattr(self.instance, 'rol', None))
        personal = attrs.get('personal',getattr(self.instance, 'personal', None))
        madre = attrs.get('madre', getattr(self.instance, 'madre', None))
        if rol == Usuario.Rol.FAMILIAR:
            if madre is None or personal is not None:
                raise serializers.ValidationError({
                    'madre':
                    'Un usuario Familiar debe estar asociado a una madre y no debe estar asociado a un personal de salud.'
                })
        if rol in [Usuario.Rol.PERSONAL_SALUD, Usuario.Rol.SUPERVISOR]:
            if personal is None or madre is not None:
                raise serializers.ValidationError({
                    'personal':
                    'Este usuario debe estar asociado a personal de salud y no debe estar asociado a un familiar.'
                })
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password: 
            instance.set_password(password)
        else:
            return 
        instance.save() 
        return instance

