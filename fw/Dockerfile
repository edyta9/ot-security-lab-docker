FROM alpine:latest

# Instalujemy iptables i podstawowe narzędzia sieciowe
RUN apk add --no-cache iptables iproute2

# Kopiujemy nasz skrypt firewall
COPY run-fw.sh /fw/run-fw.sh

RUN chmod +x /fw/run-fw.sh

# Startujemy firewall
CMD ["sh", "/fw/run-fw.sh"]
