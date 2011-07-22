import jingo
import jinja2

from waffle import flag_is_active, sample_is_active, switch_is_active


@jinja2.contextfunction
def flag_helper(context, name, output=None):
    active = flag_is_active(context['request'], name)
    if output is None:
        return active
    elif active:
        return output
    return u''


def sample_helper(name, output=None):
    active = sample_is_active(name)
    if output is None:
        return active
    elif active:
        return output
    return u''


def switch_helper(name, output=None):
    active = switch_is_active(name)
    if output is None:
        return active
    elif active:
        return output
    return u''


jingo.env.globals['waffle'] = {
    'flag': flag_helper,
    'switch': switch_helper,
    'sample': sample_helper,
}
