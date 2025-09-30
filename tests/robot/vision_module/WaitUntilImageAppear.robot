*** Settings ***
Library     src.SikuliPlusLibrary


*** Variables ***
${IMAGES_DIR}=                  ${EXECDIR}\\tests\\robot\\images
${DASHBOARD_DIR}=               ${IMAGES_DIR}\\dashboard
${COMPONENTS_DASHBOARD}=        ${DASHBOARD_DIR}\\components

${DASHBOARD}=                   ${DASHBOARD_DIR}\\dashboard.png
${dashboard_title}=             ${COMPONENTS_DASHBOARD}\\dashboard_title.png

${visits_card}=                 ${COMPONENTS_DASHBOARD}\\visits_card.png
${visits_today}=                ${COMPONENTS_DASHBOARD}\\visits_today.png

${articles_card}=               ${COMPONENTS_DASHBOARD}\\articles_card.png
${total_articles}=              ${COMPONENTS_DASHBOARD}\\total_articles.png

${tickets_card}=                ${COMPONENTS_DASHBOARD}\\tickets_card.png
${porcent_open_tickets}=        ${COMPONENTS_DASHBOARD}\\porcent_open_tickets.png

${comments_card}=               ${COMPONENTS_DASHBOARD}\\comments_card.png
${total_comments}=              ${COMPONENTS_DASHBOARD}\\total_comments.png

${article_views_graphics}=      ${COMPONENTS_DASHBOARD}\\article_views_graphics.png

${classification_chart}=        ${COMPONENTS_DASHBOARD}\\classification_chart.png


*** Test Cases ***
Only image parameter
    Wait Until Image Appear    ${DASHBOARD}
    Wait Until Image Appear    ${dashboard_title}
    Wait Until Image Appear    ${visits_card}
    Wait Until Image Appear    ${articles_card}
    Wait Until Image Appear    ${tickets_card}
    Wait Until Image Appear    ${comments_card}
    Wait Until Image Appear    ${article_views_graphics}
    Wait Until Image Appear    ${classification_chart}


Only image parameter and Timeout
    Wait Until Image Appear    ${DASHBOARD}    timeout=5
    Wait Until Image Appear    ${dashboard_title}    timeout=5


With Roi Parameter
    Wait Until Image Appear    ${visits_today}    roi=${visits_card}
    Wait Until Image Appear    ${total_articles}    roi=${articles_card}
    Wait Until Image Appear    ${total_comments}    roi=${comments_card}
    Wait Until Image Appear    ${porcent_open_tickets}    roi=${tickets_card}

With Roi Parameter and Similarity
    Wait Until Image Appear    ${visits_today}    roi=${visits_card}    similarity=0.85    
    Wait Until Image Appear    ${total_articles}    roi=${articles_card}    similarity=0.85
    Wait Until Image Appear    ${total_comments}    roi=${comments_card}    similarity=0.85
    Wait Until Image Appear    ${porcent_open_tickets}    roi=${tickets_card}    similarity=0.85
