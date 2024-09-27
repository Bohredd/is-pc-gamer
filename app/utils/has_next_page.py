def has_next_page(soup) -> bool:
    load_more_div = soup.find('div', class_='List__loadMore___2Nxfw')

    if load_more_div:
        return True

    return False
