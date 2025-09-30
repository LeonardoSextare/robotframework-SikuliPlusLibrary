# SikuliPlusLibrary

## Sobre o Projeto

A **SikuliPlusLibrary** é uma biblioteca para o Robot Framework que estende a [SikuliLibrary](https://github.com/rainmanwy/robotframework-sikulilibrary) para automação de testes de GUI por meio de reconhecimento de imagens. Ela fornece funcionalidades adicionais de automação de GUI não cobertas pela SikuliLibrary original, utilizando apenas uma instância da SikuliLibrary sem modificar seu código.

## Produto Mínimo Viável (MVP)

Este projeto está atualmente em sua fase de MVP, com foco principal no módulo de visão computacional (`vision.py`). O objetivo é estabelecer uma base sólida para expansões futuras, implementando funcionalidades essenciais de reconhecimento visual.

## Checklist de Objetivos

### Objetivos Atuais (MVP)
- [ ] Implementar base sólida para expansão futura
- [ ] Implementar funcionalidades de visão computacional (vision.py)
  - [ ] ROI Temporário
  - [ ] Similarity Temporário
  - [ ] Highlight nas imagens encontradas
- [ ] Funções iniciais:
  - [ ] Wait Until Image Appears
  - [ ] Wait One of Multiple Images Appears
  - [ ] Wait Until Multiple Images Appear
- [ ] Implementar possibilidade de escolher a tela alvo (multi-monitor)

### Planos Futuros
- [ ] Tratamento de Erros e Exceções melhorados
- [ ] Módulo de mouse (mouse.py)
- [ ] Módulo de teclado (keyboard.py)
- [ ] Suporte a múltiplas linguagens (Keywords, Docstrings, Mensagens de erro localizadas)
- [ ] Suporte a configuração global por:
  - [ ] Variáveis de ambiente
  - [ ] Arquivo de configuração (TOML)
  - [ ] Pyproject.toml
  - [ ] Argumentos na importação da biblioteca no Robot Framework
- [ ] Cobertura de testes automatizados (unitários e integração)
- [ ] Cobertura de testes no ambiente Robot Framework
- [ ] Documentação completa com libdoc
