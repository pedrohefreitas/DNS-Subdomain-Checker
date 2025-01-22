# DNS-Subdomain-Checker

Este repositório contém um script Python para verificar a existência de subdomínios a partir de uma wordlist. Ele utiliza as bibliotecas requests e tqdm para fazer requisições HTTP e exibir o progresso de forma interativa.

As bibliotecas necessárias podem ser instaladas com os seguintes comandos:

pip install tqdm
pip install requests

Prepare uma wordlist contendo os subdomínios a serem testados. Você pode utilizar uma das wordlists disponíveis nos repositórios abaixo:

https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056
https://github.com/rbsec/dnscan

O script retornará uma lista de subdomínios encontrados que estão ativos, exibindo o progresso da verificação.
