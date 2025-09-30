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
Wait for multiple images - basic
    Wait Multiple Images Appear    ${DASHBOARD}    ${dashboard_title}    timeout=10    similarity=0.8

Wait for multiple images - all cards
    Wait Multiple Images Appear    ${visits_card}    ${articles_card}    ${tickets_card}    ${comments_card}    timeout=10    similarity=0.8

Wait for multiple images with ROI
    Wait Multiple Images Appear   ${visits_today}    ${total_articles}    timeout=10    similarity=0.8    roi=${visits_card}

Wait for multiple images - dashboard components
    Wait Multiple Images Appear    ${dashboard_title}    ${article_views_graphics}    ${classification_chart}    timeout=10    similarity=0.8

Wait for multiple images - timeout scenario
    Run Keyword And Expect Error    TimeoutError*    Wait Multiple Images Appear    nonexistent1.png    nonexistent2.png    timeout=2    similarity=0.8