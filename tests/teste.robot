*** Settings ***
Resource    ${EXECDIR}\\source\\keywords.robot


*** Variables ***
${imagens}=    ${EXECDIR}\\tests\\imagens

*** Test Cases ***
Teste
    Aguardar imagem na tela       imagem=${imagens}\\txt_transferencia.png     ponto_de_interesse=${imagens}\\inovafarma.png    similaridade=0.8

    Wait Until Screen Contain    ${imagens}\\txt_transferencia.png    3
