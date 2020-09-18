from stograde.specs import get_filenames
from stograde.specs.spec import Spec
from stograde.specs.spec_file import create_spec_file


def test_get_filenames():
    spec = Spec(id='hw1', folder='hw1', architecture=None)
    spec_file1 = create_spec_file({
        'file': 'file1.txt',
    })
    spec_file2 = create_spec_file({
        'file': 'file2.txt',
    })
    spec_file3 = create_spec_file({
        'file': 'another_file.txt',
    })
    spec_file4 = create_spec_file({
        'file': 'an_optional_file.txt',
        'options': {
            'optional': True,
        },
    })
    spec.files.extend([spec_file1, spec_file2, spec_file3, spec_file4])
    assert set(get_filenames(spec)) == {'file1.txt', 'file2.txt', 'another_file.txt'}
