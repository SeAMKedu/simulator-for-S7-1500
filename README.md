# Simulaattori Siemens Simatic S7-1500 -sarjan logiikoille

Ohjelmassa on neljä liikkuvaa sylinteriä ja neljä moottoria, joita voidaan ohjata PLC:n avulla. PLC saa simulaattorilta tiedon sylinterien ja moottorien tilasta. Kommunikointi simulaattorin ja PLC:n välillä tapahtuu Snap7-kirjaston avulla.

![ui](/imgs/sim_ui.png)

## Ohjelmistoriippuvuudet

Graafinen käyttöliittymä on toteutettu [customtkinter](https://pypi.org/project/customtkinter/)-paketin avulla. [Pillow](https://pypi.org/project/pillow/)-pakettia tarvitaan sylinterin ja moottorin kuvatiedostoja varten. [python-snap](https://pypi.org/project/python-snap7/) on puolestaan wrapperi Snap7:lle.

Tarvittavat kirjastot voidaan asentaa komennolla
```
pip install -r requirements.txt
```

## PLC:n asetukset

![ip_addr](/imgs/plc_ip_addr.png)
**Kuva 1**. IP-osoitteen määritys.

![access_level](/imgs/plc_access_level.png)
**Kuva 2**. Käyttöoikeustason asetus.

![permit_putget](/imgs/plc_permit_putget.png)
**Kuva 3**. PUT/GET kommunikoinnin salliminen.

![inputs](/imgs/plc_db2_inputs.png)
**Kuva 4** Tulot (DB2).

![outputs](/imgs/plc_db3_outputs.png)
**Kuva 5** Lähdöt (DB3).

![db](/imgs/plc_db_config.png)
**Kuva 4**. Optimoinnin asetus pois päältä.

## S7-PLCSIM Advanced

![plcsim](/imgs/plcsim_adv5.png)

Aseta PLCSIM Advanced -ohjelmassa sama IP-osoite kuin PLC:ssä.

## Simulaattorin ajaminen

Simulaattori-sovellus olettaa PLC:n IP-osoitteen olevan "192.168.0.1". Se voidaan kuitenkin tarvittaessa muuttaa "PLC Config"-välilehdellä.

1. Avaa S7-PLCSIM Advanced -ohjelma ja käynnistä virtuaalinen PLC
1. Avaa TIA-Portal, luo PLC-ohjelma, ja mene Online-tilaan
1. Avaa simulaattori-sovellus komennolla
```
python simulator.py
```

Simulaattori-sovellus voidaan sulkea sovellusikkunan oikean yläkulman rastista.

## Tekijätiedot

Hannu Hakalahti, Asiantuntija TKI, Seinäjoen ammattikorkeakoulu

![seamk](/imgs/seamk.jpg)
