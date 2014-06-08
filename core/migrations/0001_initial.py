# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Superpower'
        db.create_table(u'core_superpower', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Superpower'])

        # Adding model 'Hero'
        db.create_table(u'core_hero', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Hero'])

        # Adding M2M table for field superpowers on 'Hero'
        m2m_table_name = db.shorten_name(u'core_hero_superpowers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hero', models.ForeignKey(orm[u'core.hero'], null=False)),
            ('superpower', models.ForeignKey(orm[u'core.superpower'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hero_id', 'superpower_id'])

        # Adding model 'CampaignHero'
        db.create_table(u'core_campaignhero', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(related_name='campaign_heroes', to=orm['core.Campaign'])),
            ('hero', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hero_campaigns', to=orm['core.Hero'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'core', ['CampaignHero'])

        # Adding model 'Campaign'
        db.create_table(u'core_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('location_address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('threshold', self.gf('django.db.models.fields.IntegerField')(default=8)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Hero'], null=True, blank=True)),
            ('location_lat', self.gf('core.models.DefaultDecimalField')(null=True, max_digits=20, decimal_places=8, blank=True)),
            ('location_lon', self.gf('core.models.DefaultDecimalField')(null=True, max_digits=20, decimal_places=8, blank=True)),
        ))
        db.send_create_signal(u'core', ['Campaign'])


    def backwards(self, orm):
        # Deleting model 'Superpower'
        db.delete_table(u'core_superpower')

        # Deleting model 'Hero'
        db.delete_table(u'core_hero')

        # Removing M2M table for field superpowers on 'Hero'
        db.delete_table(db.shorten_name(u'core_hero_superpowers'))

        # Deleting model 'CampaignHero'
        db.delete_table(u'core_campaignhero')

        # Deleting model 'Campaign'
        db.delete_table(u'core_campaign')


    models = {
        u'core.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'heroes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'c_campaigns+'", 'symmetrical': 'False', 'through': u"orm['core.CampaignHero']", 'to': u"orm['core.Hero']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'location_lat': ('core.models.DefaultDecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '8', 'blank': 'True'}),
            'location_lon': ('core.models.DefaultDecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '8', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Hero']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'threshold': ('django.db.models.fields.IntegerField', [], {'default': '8'})
        },
        u'core.campaignhero': {
            'Meta': {'object_name': 'CampaignHero'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'campaign_heroes'", 'to': u"orm['core.Campaign']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'hero': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hero_campaigns'", 'to': u"orm['core.Hero']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'core.hero': {
            'Meta': {'object_name': 'Hero'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'superpowers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.Superpower']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.superpower': {
            'Meta': {'object_name': 'Superpower'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']