*** Settings ***
Library    SikuliLibrary
Variables    constantes.py

*** Keywords ***

Aguardar imagem na tela
    [Arguments]    ${imagem}    ${tempo}=5    ${similaridade}=${SIMILARIDADE_MIN}    ${ponto_de_interesse}=${EMPTY}
    
    Set Min Similarity    ${similaridade}

    Highlight    ${ponto_de_interesse} 
    ${regiao}=    Get Image Coordinates    ${ponto_de_interesse}
    Set Roi    ${regiao}


    Highlight    ${imagem} 
    Sleep  2
    Wait Until Screen Contain    image=${imagem}    timeout=${tempo}

    Clear All Highlights
    Reset Roi
    Set Min Similarity    ${SIMILARIDADE_MIN}

