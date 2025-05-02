from nbconvert.preprocessors import Preprocessor

class HideCodePreprocessor(Preprocessor):
    """
    Preprocessor to hide code cells marked with hideCode: true in metadata
    """
    def preprocess_cell(self, cell, resources, cell_index):
        """
        Skip code cells that have hideCode: true in their metadata
        """
        if cell.cell_type == 'code' and cell.metadata.get('hideCode', False):
            cell.source = ''
            cell.metadata['transient'] = {
                'remove_source': True
            }
        return cell, resources