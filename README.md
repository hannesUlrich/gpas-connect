
# gPAS Connect
gPAS-Connect: Communication wrapper to use gPAS within python ETL pipelines. This library provides two clients: an AdminClient and simple Client. 
The AdminClient is able to create new domains, whereas the Client is used for pseudonomization.


### Installation 

```shell
pip install git+https://github.com/hannesUlrich/gpas-connect.git
```

### Usage

```python
from gpas_connect import Client, AdminClient

if __name__ == '__main__':

    root_domain = 'MeDIC'
    sub_domain = 'Dental_AI'

    # Create an AdminClient
    gPas_admin_client = AdminClient(base_url='http://localhost', port=8080)
    # Create root domain
    gPas_admin_client.create_domain(root_domain, alphabet=AdminClient.Alphabets.Symbol31,
                                    generator=AdminClient.Generators.NoCheckDigits)
    # Create Subdomain below the root domain
    gPas_admin_client.create_domain(sub_domain, alphabet=AdminClient.Alphabets.Symbol32,
                                    generator=AdminClient.Generators.HammingCode, parent_domain=root_domain)

    # Create gPAS client
    print('create client')
    gPas_client = Client(base_url='http://localhost', port=8080, domain=sub_domain)

    patient_id = '1234567890_HannesUlrich'

    # Create pseudonym
    pseudo = gPas_client.get_pseudonym(patient_id)
    print("Pseudo: " + pseudo)

    # Resolve the pseudonym
    print("Resolved ID: " + gPas_client.get_name(pseudo))

    # Error on resolving pseudonym
    # Unknown
    print(gPas_client.get_name("GJNW1G5080C8"))
    # To short
    print(gPas_client.get_name("GJNW"))
```

### Roadmap
- [ ] Add external configuration over conf-object 
- [ ] Add authentication headers
- [ ] Add generator restrictions
