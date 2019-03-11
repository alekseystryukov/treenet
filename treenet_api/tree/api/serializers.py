from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.fields import SerializerMethodField, ListField, DictField
from rest_framework_mongoengine.validators import ValidationError
from tree.models import Branch, BranchPost
from mongoengine import EmbeddedDocumentField


class BranchSerializer(DocumentSerializer):

    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class BranchPostSerializer(DocumentSerializer):

    class Meta:
        model = BranchPost
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop("branch")
        super(BranchPostSerializer, self).__init__(**kwargs)

    def validate_values(self, values):
        if isinstance(values, dict):
            features_dict = self.branch.features_dict

            for key, value in values.items():
                if key not in features_dict:
                    raise ValidationError("{} is not allowed option. [{}]".format(key, features_dict.keys()))

                feature = features_dict[key]

                representation = feature["representation"]
                if representation == "number":
                    try:
                        values[key] = float(value)
                    except ValueError:
                        raise ValidationError(
                            {"value": "'{}' is a wrong number".format(value)})

                elif representation == "choices":
                    value = str(value)
                    if value not in feature["choices"]:
                        raise ValidationError(
                            {"value": "'{}' is a wrong choise".format(value)})

            return values



