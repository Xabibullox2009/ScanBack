from django.db import migrations, models


def migrate_old_qr_code_to_public_code(apps, schema_editor):
    AssetContact = apps.get_model("qrhub", "AssetContact")

    for asset in AssetContact.objects.all():
        if not getattr(asset, "public_code", ""):
            asset.public_code = asset.qr_code or f"scanback-item-{asset.pk}"
        asset.qr_code = ""
        asset.save(update_fields=["public_code", "qr_code"])


def rollback_public_code_to_old_qr_code(apps, schema_editor):
    AssetContact = apps.get_model("qrhub", "AssetContact")

    for asset in AssetContact.objects.all():
        asset.qr_code = asset.public_code or ""
        asset.save(update_fields=["qr_code"])


class Migration(migrations.Migration):

    dependencies = [
        ('qrhub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetcontact',
            name='public_code',
            field=models.SlugField(blank=True, help_text='QR scan qilinganda URL ichida ishlatiladigan noyob kod.', max_length=80, null=True, verbose_name='Public kod'),
        ),
        migrations.RunPython(
            migrate_old_qr_code_to_public_code,
            rollback_public_code_to_old_qr_code,
        ),
        migrations.AlterField(
            model_name='assetcontact',
            name='public_code',
            field=models.SlugField(blank=True, help_text='QR scan qilinganda URL ichida ishlatiladigan noyob kod.', max_length=80, unique=True, verbose_name='Public kod'),
        ),
        migrations.AlterField(
            model_name='assetcontact',
            name='qr_code',
            field=models.ImageField(blank=True, help_text='Admin paneldan QR rasmni yuklang.', null=True, upload_to='qr_codes/', verbose_name='QR code rasmi'),
        ),
    ]
