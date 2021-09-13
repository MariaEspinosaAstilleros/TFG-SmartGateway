# -*- mode: makefile-gmake; coding: utf-8 -*-
DESTDIR ?= ~

all:

install:
	install -vd $(DESTDIR)/usr/bin
	install -vd $(DESTDIR)/lib/systemd/system
	install -vd $(DESTDIR)/etc/compose
	install -vd $(DESTDIR)/etc/default
	install -vd $(DESTDIR)/etc/shapes-monitoring
	install -vd $(DESTDIR)/etc/grafana/provisioning/datasources
	install -vd $(DESTDIR)/etc/grafana/provisioning/dashboards
	install -vd $(DESTDIR)/usr/share/shapes-monitoring/datasources
	install -vd $(DESTDIR)/usr/share/shapes-monitoring/dashboards
	install -vd $(DESTDIR)/var/lib/grafana/dashboards
	install -vd $(DESTDIR)/usr/share/man/man1
	install -v -m 555 client_mqtt.py $(DESTDIR)/usr/bin/shapes-monitoring-client
	install -v -m 555 shapes-monitoring $(DESTDIR)/usr/bin/shapes-monitoring 
	cp configuration.conf $(DESTDIR)/etc/shapes-monitoring
	cp grafana.ini $(DESTDIR)/etc/grafana
	cp config/systemd/shapes-monitoring.service $(DESTDIR)/lib/systemd/system/
	cp -r config/service-data/* $(DESTDIR)/etc/compose
	cp default/shapes-monitoring $(DESTDIR)/etc/default
	cp dashboards/shapes-monitoring-dashboard.json $(DESTDIR)/var/lib/grafana/dashboards
	cp dashboards/shapes-monitoring-dashboard.yaml $(DESTDIR)/etc/grafana/provisioning/dashboards
	cp datasources/shapes-monitoring-datasource.yaml $(DESTDIR)/etc/grafana/provisioning/datasources
	cp datasources/shapes-monitoring-datasource.yaml $(DESTDIR)/usr/share/shapes-monitoring/datasources
	cp dashboards/* $(DESTDIR)/usr/share/shapes-monitoring/dashboards
	cp shapes-monitoring.1 $(DESTDIR)/usr/share/man/man1
	gzip $(DESTDIR)/usr/share/man/man1/shapes-monitoring.1
