#!/bin/bash
service ssh start
service tor start
nginx -g 'daemon off;'