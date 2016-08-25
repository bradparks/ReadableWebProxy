From https://news.ycombinator.com/item?id=12346441

## Readable-Web Proxy
I do a significant amount of scraping for hobby projects, albeit mostly open websites. As a result, I've gotten pretty good a circumventing rate-limiting and most other controls.
I suspect I'm one of those bad people your parents tell you to avoid - by that I mean I completely ignore robots.txt.
At this point, my architecture has settled on a distributed RPC system with a rotating swarm of clients. I use RabbitMQ for message passing middleware, SaltStack for automated VM provisioning, and python everywhere for everything else. Using some randomization, and a list of the top n user agents, I can randomly generate about ~800K unique but valid-looking UAs. Selenium+PhantomJS gets you through non-capcha cloudflare. Backing storage is Postgres.
Database triggers do row versioning, and I wind up with what is basically a mini internet-archive of my own, with periodic snapshots of a site over time. Additionally, I have a readability-like processing layer that re-writes the page content in hopes of making the resulting layout actually pleasant to read on, with pluggable rulesets that determine page element decomposition.
At this point, I have a system that is, as far as I can tell, definitionally a botnet. The only things is I actually pay for the hosts.
---
Scaling something like this up to high volume is really an interesting challenge. My hosts are physically distributed, and just maintaining the RabbitMQ socket links is hard. I've actually had to do some hacking on the RabbitMQ library to let it handle the various ways I've seen a socket get wedged, and I still have some reliability issues in the SaltStack-DigitalOcean interface where VM creation gets stuck in a infinite loop, leading to me bleeding all my hosts. I also had to implement my own message fragmentation on top of RabbitMQ, because literally no AMQP library I found could reliably handle large (>100K) messages without eventually wedging.
There are other fun problems too, like the fact that I have a postgres database that's ~700 GB in size, which means you have to spend time considering your DB design and doing query optimization too. I apparently have big data problems in my bedroom (My home servers are in my bedroom closet).







Reading long-form content on the internet is a shitty experience.   
This is a web-proxy that tries to make it better.

This is a *rewriting proxy*. In other words, it proxies arbitrary web
content, while allowing the rewriting of the remote content as driven
by a set of rule-files. The goal is to effectively allow the complete
customization of any existing web-sites as driven by predefined rules.

Functionally, it's used for extracting just the actual content body
of a site and reproducing it in a clean layout. It also modifies
all links on the page to point to internal addresses, so following a
link points to the proxied version of the file, rather then the original.


---

Quick installation overview:

 - Install Postgresql **>= 9.5.** This is ~~alpha~~, you will (probably) have to build from source.
     (This is because this project uses the new `ON CONFLICT` clause)
 - Build the community extensions for Postgresql.
 - Create a database for the project.
 - In the project database, install the `pg_trgm` and `citext` extensions from the 
    community extensions modules.
 - Copy `settings.example.py` to `settings.py`.
 - Setup virtualhost by running `build-venv.sh`
 - Activate vhost: `source flask/bin/activate`
 - Bootstrap DB: `create_db.sh`
 - (Potentially) disable wattpad login system by editing the content of `INIT_CALLS` in 
     `activePlugins.py`.
 - Run server: `python3 run.py`
 - (Optional): Scraper is started by `python runScrape.py`
 - (Optional): Scraper periodic scheduler is started by `python runScrape.py scheduler`
