# vim: ts=4 sw=4 et fdm=indent
from datetime import datetime

from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from django.db.models.signals import post_save                                  
from django.dispatch import receiver

from geopy import geocoders

MAX_CHARFIELD_LENGTH = 255
MAX_DECIMALFIELD_PLACES = 8
MAX_DECIMALFIELD_DIGITS = 20


class Superpower(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

    def __unicode__(self):
        return self.name


class Hero(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="E-mail address",
        max_length=255,
        unique=True
    )
    username = models.CharField(
        max_length=MAX_CHARFIELD_LENGTH,
        unique=True
    )

    photo = models.ImageField(upload_to='users', null=True, blank=True,
                              verbose_name='photo')

    superpowers = models.ManyToManyField(
        Superpower, related_name='heroes', null=True, blank=True, 
        verbose_name='Skills', help_text="What could you do towards this campaign?"
    )

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_absolute_url(self):
        return reverse("hero_detail", kwargs={"username": self.username})


class DefaultDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('decimal_places', MAX_DECIMALFIELD_PLACES)
        kwargs.setdefault('max_digits', MAX_DECIMALFIELD_DIGITS)
        super(DefaultDecimalField, self).__init__(*args, **kwargs)


class CampaignHero(models.Model):
    campaign = models.ForeignKey("Campaign", related_name="campaign_heroes")
    hero = models.ForeignKey(Hero, related_name="hero_campaigns")

    public = models.BooleanField(
        verbose_name=u"Show your username and profile picture on this campaign's page?",
        default=True
    )
    date_created = models.DateTimeField(default=datetime.now, editable=False)

    def __unicode__(self, *args, **kwargs):
        return u"%s in %s" % (
            self.hero.username,
            self.campaign.name
        )


class Campaign(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    description = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

    slug = models.SlugField(max_length=MAX_CHARFIELD_LENGTH, unique=True, 
                            verbose_name='slug')

    location_address = models.CharField(max_length=MAX_CHARFIELD_LENGTH)

    threshold = models.IntegerField(default=8)
    
    date_created = models.DateTimeField(default=datetime.now, editable=False)

    owner = models.ForeignKey(Hero, blank=True, null=True, related_name='owned_campaigns')

    location_lat = DefaultDecimalField(editable=False, blank=True, null=True)
    location_lon = DefaultDecimalField(editable=False, blank=True, null=True)

    heroes = models.ManyToManyField(Hero, through=CampaignHero, 
                                    related_name='c_campaigns+')

    def __unicode__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return reverse("campaign_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """ Set location from self.location_address, if possible

        FIXME: use different geocoder service
        FIXME: handle geocoding errors gracefully
        TODO: break out to separate function to expose as API view """
        if self.location_address:
            self.location_lat, self.location_lon = map(
                str, geocoders.GoogleV3().geocode(self.location_address)[1]
            )
        super(Campaign, self).save(*args, **kwargs)


@receiver(post_save, sender=CampaignHero)
def check_campaign_threshold(sender, instance, **kwargs):
    if instance.campaign.heroes.count() >= instance.campaign.threshold:
        send_mail(
            'Campaign "%s" has hit %d members - time to act!' % (
                instance.campaign.name,
                instance.campaign.heroes.count()
            ),
            'Message text',
            'noreply@hands-up.org.uk',
            [h.email for h in instance.campaign.heroes.all()]
        )


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^core\.models\.DefaultDecimalField"])
