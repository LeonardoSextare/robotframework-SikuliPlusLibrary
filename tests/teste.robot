*** Settings ***
Library     SikuliPlusLibrary    language=pt_BR


*** Variables ***
${imagens}=    ${EXECDIR}\\tests\\imagens
@{regiao}=    100    100    100    100    
@{cords}=    28    80    237    76

*** Test Cases ***
Teste
    # ${roi}=    Capture Roi
    # Set Roi    ${regiao}    5
    # Log To Console     ${roi}

    # ${teste}=    Get Image Coordinates    ${roi}
    Log To Console     teste
    # [-1920, 376, 1920, 1080]
    
    # Highlight Region    ${teste}    1
    # Count Multiple Images    ${imagens}\\txt_transferencia.png    ${imagens}\\inovafarma.png
    
