pip install -r requirements.txt #para instalar as bibliotecas necessarias

Este script utiliza a biblioteca Selenium para automatizar o login em um site de testes chamado Swag Labs e recuperar os títulos dos produtos disponíveis na página após o login.

O código utiliza o WebDriver do Chrome, que é gerenciado automaticamente pela biblioteca webdriver-manager.

O Chrome é configurado para rodar em modo "headless" (sem abrir uma janela visível), otimizando a execução do teste no terminal.

Um conjunto de opções é configurado para o navegador, como maximizar a tela e desativar o uso de sandbox e memória compartilhada.

O script acessa a página inicial do site Swag Labs e extrai a lista de nomes de usuários disponíveis a partir de um elemento XPATH.

Filtra essa lista para eliminar os títulos e obter apenas os nomes utilizáveis.

A senha é fixada como "secret_sauce" para todos os usuários, pois o site de testes usa a mesma senha para todos.

Para cada usuário, o script tenta realizar o login preenchendo o campo de nome de usuário e senha e clicando no botão de login.

Se o usuário estiver bloqueado (indicado pela presença de um elemento específico na página após a tentativa de login), o script tenta outro nome de usuário.

Após um login bem-sucedido, o script localiza e coleta os títulos de até 5 produtos disponíveis na página de inventário.

Esses títulos são armazenados em uma lista.

Após coletar os títulos de produtos, o script retorna à página inicial do site para testar o próximo usuário.

O processo se repete até que todos os usuários disponíveis tenham sido testados.

O script mantém um contador de quantos usuários já foram testados e imprime mensagens no terminal, como o número do usuário que está sendo testado e os títulos recuperados.

Para cada usuário, os dados de login (nome de usuário, senha) e os títulos dos produtos são formatados e impressos em formato JSON.

Quando todos os usuários tiverem sido testados, o script finaliza com a mensagem: "Teste com X usuários concluídos.", onde X é o número total de usuários testados. 
