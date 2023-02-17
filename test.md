The following is the pseudo-code for the Sugiyama algorithm.

```
Procedure: ordering()
    order = init_order();
    best=order;
    for i = 0 to Max-iterationsdo
        wmedian(0rder.i);
        transpose(0rder);
        if crossing(0rder) < crossing(best) then:
            best = order;
    end
    return best
end

Procedure: wmedian(order)
    for i = 0 to n-1 do
        order.i = median(order.i);
    end
end

Procedure: transpose(order)
    for i = 0 to n-1 do
        order.i = transpose(order.i);
    end
end
```