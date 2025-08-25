*** Settings ***
Library    SikuliLibrary
Variables    constantes.py

*** Keywords ***

Aguardar imagem na tela
    [Arguments]    ${imagem}    ${tempo}=5    ${ponto_de_interesse}=${EMPTY}     ${similaridade}=${SIMILARIDADE_MIN}
    
    Set Min Similarity    ${similaridade}
    ${regiao}=    Get Image Coordinates    ${ponto_de_interesse}
    Set Roi    ${regiao}    5


    Highlight    ${imagem}   1 
    Wait Until Screen Contain    image=${imagem}    timeout=${tempo}

    Set Min Similarity    ${SIMILARIDADE_MIN}

