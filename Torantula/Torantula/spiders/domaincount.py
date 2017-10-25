

class DomainCount(object):
    """
    Class to keep track of domain counts during a scrape. This class upkeeps
    a constantly updated dictionary formatted as {domain: domain_count}
    """

    IGNORE_COUNT = 20

    def __init__(self):
        """
        Initialize the class with an empty dictionary
        """

        self.domains = {}

    def get_domains(self):
        """
        :return: The entire domain count dictionary
        """

        return self.domains

    def get_domain_count(self, domain):
        """
        Get the current visit-count for a specific domain
        :param domain: The domain to check against the dictionary
        :return: The visit-count that matches the passed domain
        """

        return self.domains[domain]

    def get_ignored_domains(self):
        """
        Get all domains in a list that have been visited too many times
        :return: A list of domains that have been visited too many times
        """

        igd = []
        for domain in self.domains.keys():
            if self.domains[domain] >= self.IGNORE_COUNT:
                igd.append(domain)
        return igd

    def update_domain(self, domain):
        """
        Increment the domain count for a specific domain. Initialize the domain
        in the dictionary if it isn't already present.
        :param domain: The domain to update
        """

        if domain in self.domains:
            self.domains[domain] += 1
        else:
            self.domains[domain] = 1

    def set_ignored_domain(self, domain):
        """
        Set a domain to have been visited too many times, which indicates that
        it should be ignored.
        :param domain: The domain to set to be ignored
        """

        self.domains[domain] = self.IGNORE_COUNT

    def ignore_this(self, domain):
        """
        Rerturn true if a single domain should be ignored
        :param domain: The domain to test for IGNORING
        :return: True if the domain has been visited too many times
        """

        if domain in self.domains.keys():
            return self.domains[domain] >= self.IGNORE_COUNT
