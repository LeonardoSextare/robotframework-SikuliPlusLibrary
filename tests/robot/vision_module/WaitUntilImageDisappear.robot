*** Settings ***
Library     SikuliPlusLibrary


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
Wait until image disappear - basic
    Wait Until Image Dissapear    ${DASHBOARD}    timeout=10    similarity=0.8

Wait until image disappear with ROI
    Wait Until Image Dissapear    ${visits_today}    timeout=10    similarity=0.8    roi=${visits_card}

Wait until image disappear - timeout scenario
    Wait Until Image Dissapear    nonexistent.png    timeout=2    similarity=0.8