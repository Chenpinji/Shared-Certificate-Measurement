# Shared Certificate Measurement
This repo aims to conduct a large-scale shared certificate measurement on Tranco Top 1K(We also conducted measurement on Alexa Top 1K, though Alexa stopped updating their rank). We managed to find which websites are sharing TLS/SSL certificates with Tranco's Top 1K websites. By analyzing the rank of these "related websites", we reveal the rank dependency phenomenon of today's certificate ecosystem. 

## Summay
* ***Alexa***  contains the code, dataset, and result of measurement on the latest Alexa Top 1K. We are not going to maintain it as Alexa rank is disappearing.

* ***Tranco_Dateset*** includes Tranco Top1m(without subdomain) and Tranco Top1m(with subdomain ) downloaded from the official website on 2023-11-18.

* ***Tranco_SAN*** measures the Tranco Top1W's SSL/TLS certificate and records their CN as well as SAN.

* ***Tranco1K_relate_domain*** collects Tranco Top 1K related domains as many as possible. 

* ***Tranco_secure_dep*** filters the domains that shared certificates with Tranco Top 1K from the related domains. By checking each domain's rank, we reveal the rank dependency phenomenon.


## Shared Certificate 
please go to Tranco1K_relate_domain to check our codes and measurement result. 
At last, we identified 99827 related domains. ***63577 / 99827*** domains server certificate on 443 port and ***45930 / 63577*** domains share certificate with Tranco Top 1K. 


## Rank Dependency
please go to Tranco_secure_dep to check our codes and measurement results.
* ***rank_dependency_Apex.json*** gives the result of Which websites Tranco's Top 1K websites share certificates with. We use Tranco Top 1M(without subdomains) to rank these domains. 
* ***rank_dependency_Withsub.json*** since Tranco Top 1M(without subdomains) doesn't give rank to the subdomains. Thus, We use tranco Top 1M(with subdomains) to rank them and demonstrate the rank dependency phenomenon.   
* In our results, domain A depends on domain B means A is in the SAN list of B's TLS certificate. In this case, B can use server push to attack A. 

## Requirements
* Python 3.6
* Chinese developers need to bypass GFW
