#!make
.DEFAULT_GOAL=up

compose := docker-compose -f docker-compose.yml -f standalone.yml

up:
	@$(compose) up -d

reset:
	@$(compose) stop
	@$(compose) rm
	# @docker rmi beats/filebeat beats/packetbeat beats/celerybeat beats/metricbeat
	@$(compose) up -d

logs:
	@$(compose) logs -f

.PHONY: up reset logs
