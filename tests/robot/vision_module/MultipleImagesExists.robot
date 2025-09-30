*** Settings ***
Library     SikuliPlusLibrary
Library     Collections


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
Multiple images exists - all found
    ${result}=    Multiple Images Exists    ${DASHBOARD}    ${dashboard_title}    timeout=10    similarity=0.8
    Dictionary Should Contain Item    ${result}    ${DASHBOARD}    ${True}
    Dictionary Should Contain Item    ${result}    ${dashboard_title}    ${True}

Multiple images exists - partial results
    ${result}=    Multiple Images Exists    ${visits_card}    ${articles_card}    nonexistent.png    timeout=5    similarity=0.8
    Dictionary Should Contain Item    ${result}    ${visits_card}    ${True}
    Dictionary Should Contain Item    ${result}    ${articles_card}    ${True}
    Dictionary Should Contain Item    ${result}    nonexistent.png    ${False}

Multiple images exists with ROI
    ${result}=    Multiple Images Exists    ${visits_today}    ${total_articles}    timeout=10    similarity=0.8    roi=${visits_card}
    Dictionary Should Contain Item    ${result}    ${visits_today}    ${True}
    Dictionary Should Contain Item    ${result}    ${total_articles}    ${False}

Multiple images exists - timeout scenario
    ${result}=    Multiple Images Exists    nonexistent1.png    nonexistent2.png    timeout=2    similarity=0.8
    Dictionary Should Contain Item    ${result}    nonexistent1.png    ${False}
    Dictionary Should Contain Item    ${result}    nonexistent2.png    ${False}