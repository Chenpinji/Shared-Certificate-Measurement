# ca-measurement

## Rank Dependency
please go to rank_dependency_new to check our meaurement results.
* ***rank_dependency_new.json*** gives the result of Which websites do Alexa Top1K websites share certificates with. We use Alexa to rank these domains. 
* ***rank_dep_tranco.json*** are the result filtered from ***rank_dependency_new.json*** since Alexa doesn't give rank to the subdomains. Thus, We use tranco1M(including subdomains) to rank it and demonstrate the rank dependency phenomenon.   
* In our results, domain A depends on domain B means A is in the SAN list of B's TLS certificate. In this case, B can use server push to attack A. 