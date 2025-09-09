*** Settings ***
Library     SikuliPlusLibrary
Library     SikuliLibrary


*** Variables ***
${imagens}=    ${EXECDIR}\\tests\\imagens
@{regiao}=    100    100    100    100    
@{cords}=    28    80    237    76

*** Test Cases ***
Teste
    # Wait Until Image Appear    ${imagens}\\txt_transferencia.png
    # Image Exists        ${imagens}\\txt_transferencia.png

    Wait One Of Multiple Images    ${imagens}\\txt_transferencia.png
    Change Screen Id    1
    Count Image    ${imagens}\\txt_transferencia.png
    # Count Multiple Images   ${imagens}\\txt_transferencia.png     ${imagens}\\txt_transferencia.png     ${imagens}\\inovafarma.png     ${imagens}\\btn_vendas.png

    # Wait Until Screen Contain    ${imagens}\\txt_transferencia.png    3
