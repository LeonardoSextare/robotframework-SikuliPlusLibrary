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
Wait for one of multiple images - basic
    ${found_image}=    Wait One Of Multiple Images    ${DASHBOARD}    ${dashboard_title}    timeout=10    similarity=0.8
    Should Be Equal    ${found_image}    ${DASHBOARD}

Wait for one of multiple images with ROI
    ${found_image}=    Wait One Of Multiple Images    ${visits_today}    ${total_articles}    timeout=10    similarity=0.8    roi=${visits_card}
    Should Be Equal    ${found_image}    ${visits_today}

Wait for one of multiple images - multiple options
    ${found_image}=    Wait One Of Multiple Images    ${visits_card}    ${articles_card}    ${tickets_card}    ${comments_card}    timeout=10    similarity=0.8
    Should Contain    ${found_image}    card.png

Wait for one of multiple images - timeout scenario
    Run Keyword And Expect Error    TimeoutError*    Wait One Of Multiple Images    nonexistent1.png    nonexistent2.png    timeout=2    similarity=0.8