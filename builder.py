import os
import sys
import argparse
from pathlib import Path
import shutil

def create_symbolic_links(theme_path=None):
    """
    Cria links simbólicos dos arquivos do componente para o tema Shopify.
    Os links são criados para os diretórios: assets, sections e snippets.
    
    Args:
        theme_path (str): Caminho para o diretório raiz do tema Shopify
    """
    # Determinar o caminho do componente atual
    component_path = os.path.dirname(os.path.abspath(__file__))
    component_name = os.path.basename(component_path)
    
    # Se theme_path não for fornecido, tentar descobrir automaticamente
    if not theme_path:
        # Ajustado para considerar que o componente está dentro da pasta 'components'
        possible_theme_path = os.path.dirname(os.path.dirname(component_path))
        if os.path.exists(possible_theme_path) and os.path.isdir(possible_theme_path):
            theme_path = possible_theme_path
        else:
            print("Erro: Não foi possível determinar o caminho do tema Shopify automaticamente.")
            print("Por favor, forneça o caminho como argumento usando --theme-path")
            sys.exit(1)
    
    print(f"Criando links simbólicos para o componente '{component_name}'")
    print(f"Componente: {component_path}")
    print(f"Tema: {theme_path}")
    
    # Diretórios para criar links simbólicos
    directories = ['assets', 'sections', 'snippets']
    
    # Para cada diretório, verificar se existe no componente e criar links simbólicos
    for directory in directories:
        component_dir = os.path.join(component_path, directory)
        theme_dir = os.path.join(theme_path, directory)
        
        # Verificar se o diretório existe no componente
        if not os.path.exists(component_dir) or not os.path.isdir(component_dir):
            print(f"Pulando '{directory}': não existe no componente")
            continue
        
        # Criar o diretório de destino se não existir
        if not os.path.exists(theme_dir):
            os.makedirs(theme_dir)
            print(f"Diretório criado: {theme_dir}")
            
        # Criar links simbólicos para cada arquivo no diretório do componente
        files_linked = 0
        for item in os.listdir(component_dir):
            source = os.path.join(component_dir, item)
            target = os.path.join(theme_dir, item)
            
            # Pular se não for um arquivo
            if not os.path.isfile(source):
                continue
                
            # Remover o link existente ou arquivo antes de criar um novo
            if os.path.exists(target):
                if os.path.islink(target):
                    os.unlink(target)
                    print(f"Removido link existente: {target}")
                else:
                    backup = f"{target}.bak"
                    shutil.move(target, backup)
                    print(f"Arquivo existente movido para: {backup}")
            
            # Criar o link simbólico
            os.symlink(source, target)
            print(f"Link criado: {source} -> {target}")
            files_linked += 1
        
        print(f"Total de {files_linked} arquivos vinculados no diretório '{directory}'")
    
    print("\nLinks simbólicos criados com sucesso!")
    print("Agora você pode editar os arquivos no diretório do componente e ver as alterações no tema.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Criar links simbólicos do componente para o tema Shopify')
    parser.add_argument('--theme-path', type=str, help='Caminho para o diretório raiz do tema Shopify')
    
    args = parser.parse_args()
    create_symbolic_links(args.theme_path)